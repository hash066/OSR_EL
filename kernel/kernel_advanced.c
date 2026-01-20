#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/sched/signal.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/kprobes.h>
#include <linux/kallsyms.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Antigravity");
MODULE_DESCRIPTION("Advanced Rootkit Detection Module - Phase 1");

unsigned long **sys_call_table_ptr = NULL;
unsigned long original_hash = 0;

/* Simple hash function for syscall table */
static unsigned long hash_syscall_table(unsigned long **sct) {
    unsigned long hash = 0;
    int i;
    for (i = 0; i < 300; i++) { // Check first 300 syscalls
        hash ^= (unsigned long)sct[i];
    }
    return hash;
}

/* Cross-View Process Discovery */
static void detect_hidden_processes(void) {
    struct task_struct *task;
    char path[32];
    struct file *f;

    rcu_read_lock();
    for_each_process(task) {
        snprintf(path, sizeof(path), "/proc/%d", task->pid);
        f = filp_open(path, O_RDONLY, 0);
        if (IS_ERR(f)) {
            // Process exists in kernel list but NOT in /proc
            printk(KERN_WARNING "SEC_MON_HIDDEN_PROC: PID=%d (%s) hidden from /proc!\n", task->pid, task->comm);
        } else {
            filp_close(f, NULL);
        }
    }
    rcu_read_unlock();
}

/* Syscall Integrity Check */
static void check_syscall_integrity(void) {
    if (!sys_call_table_ptr) return;

    unsigned long current_hash = hash_syscall_table(sys_call_table_ptr);
    if (current_hash != original_hash) {
        printk(KERN_WARNING "SEC_MON_SYSCALL_HOOK: Syscall table hash mismatch! Modification detected.\n");
        // Could iterate to find which one changed
    }
}

static int __init adv_detector_init(void) {
    printk(KERN_INFO "SEC_MON_INFO: Advanced Detector Phase 1 Loaded\n");

    // Find syscall table (harder way if kallsyms_lookup_name is available)
    sys_call_table_ptr = (unsigned long **)kallsyms_lookup_name("sys_call_table");
    
    if (sys_call_table_ptr) {
        original_hash = hash_syscall_table(sys_call_table_ptr);
        printk(KERN_INFO "SEC_MON_INFO: Syscall table monitored at %p\n", sys_call_table_ptr);
    } else {
        printk(KERN_ERR "SEC_MON_ERROR: Could not locate sys_call_table\n");
    }

    detect_hidden_processes();
    check_syscall_integrity();

    return 0;
}

static void __exit adv_detector_exit(void) {
    printk(KERN_INFO "SEC_MON_INFO: Advanced Detector Phase 1 Unloaded\n");
}

module_init(adv_detector_init);
module_exit(adv_detector_exit);
