# Minimal metrics
## Memory
mem_usage : Amount of memory used by the container.
mem_max_usage : Maximum amount of memory used by the container.
mem_limit : Maximum amount of memory the container can use.
mem_percent : Percentage of memory used by the container.
## CPU
cpu_cpus : Number of online CPUs.
## Block I/O
blkio_bytes_read_tot : Total amount of bytes read by the cointainer.
blkio_bytes_write_tot : Total amount of bytes written by the cointainer.
## Others
update_time_seconds : Time it took to update the metrics of the container.

# Standard
## Memory
mem_cache : The amount of memory used by the processes of this control group that can be associated precisely with a block on a block device.
mem_rss : The amount of memory that doesn’t correspond to anything on disk: stacks, heaps, and anonymous memory maps.
mem_mapped_file : Indicates the amount of memory mapped by the processes in the control group.
mem_pgfault : Indicate the number of times that a process of the cgroup triggered a “page fault”.
mem_pgmajfault : Indicate the number of times that a process of the cgroup triggered a “major fault”.
mem_active_anon : The amount of anonymous memory that has been identified as active by the kernel.
mem_inactive_anon : The amount of anonymous memory that has been identified as inactive by the kernel.
mem_active_file : The amount of cache memory that has been identified as active by the kernel.
mem_inactive_file : The amount of cache memory that has been identified as inactive by the kernel.
mem_unevictable : The amount of memory that cannot be reclaimed.
## CPU
cpu_user_seconds : Amount of time a process has direct control of the CPU, executing process code.
cpu_system_seconds : Amount of time the kernel is executing system calls on behalf of the process.
#cpu_total_usage_seconds : Total amount of time the container is using the CPU.
#cpu_system_cpu_usage_seconds : Total amount of time the CPU has been executing code.
## Block I/O
blkio_bytes_read : Number of bytes read.
blkio_bytes_write : Number of bytes written.
blkio_io_read : Number of reads.
blkio_io_write : Number of writes.

# Extended
## Memory
mem_dirty
mem_hierarchical_memory_limit
mem_pgpgin
mem_pgpgout
mem_rss_huge
mem_total_active_anon
mem_total_active_file
mem_total_cache
mem_total_dirty
mem_total_inactive_anon
mem_total_inactive_file
mem_total_mapped_file
mem_total_pgfault
mem_total_pgmajfault
mem_total_pgpgin
mem_total_pgpgout
mem_total_rss
mem_total_rss_huge
mem_total_unevictable
mem_total_writeback
mem_writeback
## CPU
cpu_percpu_usage_seconds
cpu_throttling_periods
cpu_throttled_periods
cpu_throttled_time
## Block I/O
blkio_bytes_sync : Number of syncronous I/O.
blkio_bytes_async : Number of asyncronous I/O.
blkio_bytes_discard
blkio_bytes_total
blkio_io_sync : Number of syncronous R/W.
blkio_io_async : Number of asyncronous R/W.
blkio_io_discard
blkio_io_total
