import random
import sys
from collections import deque, OrderedDict

def generate_reference_string(length=20, page_range=10):
    """Generate a random page reference string"""
    return [random.randint(0, page_range-1) for _ in range(length)]

def fifo(page_frames, reference_string):
    """FIFO page replacement algorithm"""
    frames = set()
    queue = deque()
    page_faults = 0
    
    for page in reference_string:
        if page not in frames:
            page_faults += 1
            if len(frames) >= page_frames:
                removed_page = queue.popleft()
                frames.remove(removed_page)
            frames.add(page)
            queue.append(page)
    
    return page_faults

def lru(page_frames, reference_string):
    """LRU page replacement algorithm"""
    frames = set()
    lru_cache = OrderedDict()
    page_faults = 0
    
    for page in reference_string:
        if page not in frames:
            page_faults += 1
            if len(frames) >= page_frames:
                # Remove the least recently used page
                lru_page, _ = lru_cache.popitem(last=False)
                frames.remove(lru_page)
            frames.add(page)
        else:
            # Move to end to mark as most recently used
            lru_cache.pop(page)
        
        lru_cache[page] = None  # Add to end as most recently used
    
    return page_faults

def opt(page_frames, reference_string):
    """Optimal page replacement algorithm"""
    frames = set()
    page_faults = 0
    
    for i, page in enumerate(reference_string):
        if page not in frames:
            page_faults += 1
            if len(frames) >= page_frames:
                # Find the page that won't be used for the longest time
                farthest = -1
                victim = None
                for frame in frames:
                    # Find next occurrence of this frame
                    try:
                        next_use = reference_string[i+1:].index(frame)
                    except ValueError:
                        victim = frame
                        break
                    
                    if next_use > farthest:
                        farthest = next_use
                        victim = frame
                
                frames.remove(victim)
            frames.add(page)
    
    return page_faults

def main():
    page_frames = 3  # Change this number as needed
    ref_string = generate_reference_string()
    print(f"Generated reference string: {ref_string}")
    print(f"Number of page frames: {page_frames}")
    
    fifo_faults = fifo(page_frames, ref_string)
    lru_faults = lru(page_frames, ref_string)
    opt_faults = opt(page_frames, ref_string)
    
    print("\nResults:")
    print(f"FIFO page faults: {fifo_faults}")
    print(f"LRU page faults: {lru_faults}")
    print(f"OPT page faults: {opt_faults}")

if __name__ == "__main__":
    main()