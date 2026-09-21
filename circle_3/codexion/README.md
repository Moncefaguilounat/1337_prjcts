*This project has been created as part of the 42 curriculum by mouaguil.*

# Codexion

## Description

Codexion is a POSIX threads simulation of coders sharing a circular set of
limited USB dongles. A coder must reserve both neighbouring dongles before
compiling. After compiling, the coder debugs, refactors, and requests the two
dongles again. A dongle becomes temporarily unavailable after release because
of its configured cooldown.

The project demonstrates concurrent programming in C: thread creation,
mutual exclusion, scheduling, shared-state protection, and controlled
termination. The simulation stops when every coder has compiled the requested
number of times or when the monitor detects a burnout.

## Instructions

### Build

From the repository root:

```sh
make
```

The Makefile builds the `codexion` executable with:

```text
-Wall -Wextra -Werror -pthread
```

Useful maintenance rules are:

```sh
make clean
make fclean
make re
```

### Run

```sh
./codexion number_of_coders time_to_burnout time_to_compile \
    time_to_debug time_to_refactor number_of_compiles_required \
    dongle_cooldown scheduler
```

All durations are expressed in milliseconds.

| Argument | Meaning |
| --- | --- |
| `number_of_coders` | Number of coder threads and dongles. |
| `time_to_burnout` | Maximum time allowed between compilation starts. |
| `time_to_compile` | Duration of the compilation phase. |
| `time_to_debug` | Duration of the debugging phase. |
| `time_to_refactor` | Duration of the refactoring phase. |
| `number_of_compiles_required` | Number of compilations required from every coder. |
| `dongle_cooldown` | Time a released dongle remains unavailable. |
| `scheduler` | `fifo` or `edf`. |

Example:

```sh
./codexion 5 3000 200 200 200 10 800 fifo
```

The program rejects invalid arguments, including missing arguments, negative
values, non-numeric values, and scheduler values other than `fifo` or `edf`.

### Scheduler policies

- `fifo`: the request that entered the shared queue first has priority.
- `edf`: the coder with the earliest deadline has priority. Its deadline is
  `last_compile_start + time_to_burnout`.

The scheduler only selects a coder when both of its dongles are available and
their cooldowns have expired. The output uses the required state format, for
example:

```text
0 1 has taken a dongle
0 1 has taken a dongle
0 1 is compiling
200 1 is debugging
400 1 is refactoring
```

## Design overview

Each coder owns a thread and has a left and right dongle. Coders do not lock a
first dongle and then wait for the second one. Instead, a coder inserts one
request into the shared priority queue and sleeps on a condition variable. The
monitor thread is the only scheduler: it chooses an eligible request, reserves
both dongles as one operation, then wakes the coder allowed to compile. The
monitor itself does not wait on that condition variable. It repeatedly checks
for burnout and schedulable requests, using short sleeps until the nearest
known cooldown or burnout event.

Coder threads are created one at a time. During startup, the creator waits
until each new coder has inserted its first queue request before creating the
next one. This makes the initial FIFO insertion order deterministic before the
monitor starts scheduling.

The priority queue is a binary min-heap. A heap node stores a coder id, a
policy priority, and an insertion-order value. The insertion order makes FIFO
deterministic when two requests are made in the same millisecond.

## Blocking cases handled

- **Mutual exclusion:** every dongle has an availability state protected by
  mutexes, so it cannot be assigned to two coders simultaneously.
- **Deadlock prevention:** the scheduler reserves both dongles together. A
  coder never holds one dongle while waiting for another, which removes the
  hold-and-wait condition. When two dongle mutexes are needed, they are locked
  in ascending index order, preventing circular wait.
- **FIFO and EDF arbitration:** waiting coders are stored in one shared heap.
  FIFO uses request order; EDF uses the nearest compilation deadline.
- **Cooldown handling:** releasing a dongle records `released_at`. The
  scheduler refuses to reserve it until `dongle_cooldown` milliseconds have
  passed.
- **Priority reservation:** if the highest-priority request has both dongles
  free but is waiting for their cooldown, a lower-priority request cannot take
  either of those dongles and create another full cooldown delay.
- **Starvation control:** the scheduler evaluates every queued coder that is
  currently eligible; EDF uses the earliest deadline rather than an arbitrary
  thread order. Feasible parameters are still required.
- **Burnout monitoring:** a separate monitor uses raw `gettimeofday()` values
  and the strict rule `elapsed > time_to_burnout`. No grace period is added.
  Burnout is checked before scheduling, so a request cannot be granted after
  its deadline has already passed.
- **Deadline-aware monitor polling:** the monitor calculates the nearest known
  cooldown expiry or burnout time. While that event is more than one
  millisecond away, it sleeps for 100 microseconds and recalculates on its next
  loop. During the final millisecond it spins until the target time. The
  monitor rechecks burnout and the scheduler rechecks dongle cooldowns, so an
  early poll never grants a resource early. The monitor does not wait on
  `resource_cond`.
- **Precise phase timing:** reserving both dongles is the real compilation
  start. The start timestamp is saved at that atomic transition, and the coder
  waits until `start + time_to_compile`, so thread wakeup or logging delay does
  not incorrectly extend the compilation phase.
- **Serialized logs:** a dedicated log mutex covers one complete line, so
  messages from different threads cannot interleave.
- **Clean shutdown:** the shared stop flag makes coder and monitor threads
  leave their loops; created threads are joined and allocated memory/mutexes
  are released during cleanup.

## Thread synchronization mechanisms

This implementation uses `pthread_mutex_t` and `pthread_cond_t`. The mutexes
protect shared state; the condition variable lets waiting coder threads sleep
without repeatedly polling the scheduler.

| Mechanism | Shared data protected | Role |
| --- | --- | --- |
| `resource_mutex` | Heap queue, dongle availability, release timestamps, `dongles_reserved` | Makes the scheduler's check-and-reserve operation atomic. |
| Per-dongle mutex | One dongle's stored state | Protects a dongle while its availability state is updated. |
| `coder_mutex` | `last_compile_time`, `compile_count` | Lets the monitor read a coder's deadline data safely while the coder updates it. |
| `simulation_mutex` | `simulation_over` | Provides one thread-safe stop decision for all threads. |
| `log_mutex` | Standard output | Keeps each state message whole and ordered. |
| `resource_cond` | Waiting coder threads | Makes coders recheck their protected grant/stop conditions after queue, reservation, release, or stop changes. |

### Condition-variable communication

When a coder wants to compile, it locks `resource_mutex`, inserts itself into
the heap, and sets `dongles_reserved` to `0`. It then waits on
`resource_cond`. The monitor locks the same mutex, removes the chosen heap
entry, reserves both dongles, and sets that coder's `dongles_reserved` to `1`.

Requests, grants, releases, and simulation stop broadcast `resource_cond`.
Only coder threads wait on it. The monitor neither sleeps on this condition
variable nor receives its broadcasts; it notices resource changes during its
next short polling iteration. A coder always rechecks `dongles_reserved` and
the simulation stop flag in a loop while holding `resource_mutex`, which
handles harmless spurious wakeups correctly. Permission to compile is
therefore communicated through a protected shared flag, and no thread can
observe a half-completed reservation.

The key race condition prevented here is two coders observing the same pair of
dongles as available. Every scheduler caller performs the complete sequence:

```text
check both dongles -> check both cooldowns -> remove queue entry
-> reserve both dongles -> grant the coder permission
```

Because `resource_mutex` remains locked for that sequence, another thread
cannot reserve either dongle in the middle of the decision.

## Resources

- [POSIX Threads overview](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/pthread.h.html)
- [POSIX pthread_mutex_lock](https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_lock.html)
- [POSIX pthread_create](https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_create.html)
- [POSIX gettimeofday](https://pubs.opengroup.org/onlinepubs/9699919799/functions/gettimeofday.html)
- [The Open Group Base Specifications](https://pubs.opengroup.org/onlinepubs/9699919799/)

### AI use disclosure

AI was used as a learning and review assistant. It helped extract and summarize
the supplied subject , explain POSIX-thread concepts,
identify concurrency edge cases, propose test commands, and review Helgrind,
DRD, and memory-check output. All generated suggestions were reviewed,
adapted, compiled, and tested locally by the project author, who remains
responsible for understanding and defending the implementation.
