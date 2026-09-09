from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import DiskImageResource, FileResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
from gem5.simulate.exit_event import ExitEvent


requires(isa_required=ISA.X86, kvm_required=True)

from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)

cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="16kB", l1i_size="16kB", l2_size="256kB"
)

memory = SingleChannelDDR3_1600(size="3GB")

processor = SimpleProcessor(
    cpu_type=CPUTypes.KVM,
    isa=ISA.X86,
    num_cores=2,
)

for proc in processor.cores:
    proc.core.usePerf = False

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

disk_img = DiskImageResource("/home/srinija/gem5_bootcamp_2024_lab/gem5/configs/CustomFS/disk-image-ubuntu-24-04/x86-ubuntu-24-04-gapbs")
kernel = FileResource("/home/srinija/gem5chips/gem5/configs/CustomFS/disk-image-ubuntu-24-04/vmlinux-x86-ubuntu-6.8.0-52-generic")

board.set_kernel_disk_workload(
    disk_image=disk_img,
    kernel=kernel,
    kernel_args=[
        "earlyprintk=ttyS0",
        "console=ttyS0",
        "lpj=7999923",
        "root=/dev/sda2"
    ]
)

board.append_kernel_arg("interactive=true")

# Keep your exit event handler simple
def exit_event_handler():
    print("Exit event triggered - continuing simulation")
    yield False  # Always continue, never exit

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler()
    },
)

simulator.run()