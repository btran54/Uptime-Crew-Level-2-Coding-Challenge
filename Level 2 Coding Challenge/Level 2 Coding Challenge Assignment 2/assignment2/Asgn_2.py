import threading
import queue
import time
from typing import List, Union

# Helper Functionts

def print_section_header(title, width=60):
    print("\n" + "=" * width)
    print(title)
    print("=" * width)

def print_status(actor, action, details=""):
    print(f"[{actor}] {action}{': ' + details if details else ''}")

def print_notification(actor, message):
    print(f"[{actor}] !!! {message}")

def print_completion(actor):
    print(f"[{actor}] O Finished")

def verify_containers(source, destination):
    checks = []
    
    length_match = len(source) == len(destination)
    checks.append(("Length match", length_match, 
                   f"{len(source)} elements" if length_match else 
                   f"Source: {len(source)}, Destination: {len(destination)}"))
    
    order_preserved = source == destination
    checks.append(("Elements in order", order_preserved, 
                   "All correct" if order_preserved else "Mismatches found"))
    
    all_present = sorted(source) == sorted(destination)
    checks.append(("All elements present", all_present,
                   "Complete" if all_present else "Missing or duplicated"))
    
    passed = [c for c in checks if c[1]]
    failed = [c for c in checks if not c[1]]
    
    return all(c[1] for c in checks), checks, passed, failed


class ProducerConsumer:
    def __init__(self, source_data: List[Union[int, float]]):
        # Task 1: Source container with integers and doubles
        self.source_container = source_data.copy()
        source_capacity = len(self.source_container)
        
        # Task 2: Destination container with same capacity
        self.destination_container = []
        
        # Task 3: Queue with half the capacity of source
        queue_capacity = source_capacity // 2
        self.shared_queue = queue.Queue(maxsize=queue_capacity)
        
        self.lock = threading.Lock()
        self.producer_done = threading.Event()
        
        print("Initialized:")
        print(f"  Source capacity: {source_capacity}")
        print(f"  Queue capacity: {queue_capacity}")
        print(f"  Source data: {self._format_list_preview(self.source_container)}")
    
    # Task 4: Producer reads from source container into queue and notifies consumer when queue is full
    def producer(self):
        print_status("Producer", "Starting...")
        
        for number in self.source_container:
            self.shared_queue.put(number)           
            print_status("Producer", "Produced", 
                        f"{number} (Queue: {self.shared_queue.qsize()}/{self.shared_queue.maxsize})")
                        
            if self.shared_queue.full():
                print_notification("Producer", "Queue is FULL! Consumer notified")           
            time.sleep(0.01)
        
        self.producer_done.set()
        print_completion("Producer")
    
    # Task 5: Consumer reads from queue into destination container and notifies producer when queue is empty
    def consumer(self):
        print_status("Consumer", "Starting...")
        
        while True:
            try:
                number = self.shared_queue.get(timeout=0.1)
                
                with self.lock:
                    self.destination_container.append(number)
                    dest_size = len(self.destination_container)
                
                print_status("Consumer", "Consumed", 
                           f"{number} (Destination: {dest_size}/{len(self.source_container)})")
                
                if self.shared_queue.empty():
                    print_notification("Consumer", "Queue is EMPTY. Producer notified !!!")
                
                self.shared_queue.task_done()                
                time.sleep(0.015)
                
            except queue.Empty:
                if self.producer_done.is_set() and self.shared_queue.empty():
                    print_completion("Consumer")
                    break
    
    def run(self):
        producer_thread = threading.Thread(target=self.producer, name="Producer")
        consumer_thread = threading.Thread(target=self.consumer, name="Consumer")
        
        consumer_thread.start()
        producer_thread.start()
        
        producer_thread.join()
        consumer_thread.join()
    
    # Task 6: Test to confirm numbers from source were copied to destination
    def verify(self) -> bool:
        print_section_header("Verification Results")
        
        success, all_checks, passed, failed = verify_containers(
            self.source_container, 
            self.destination_container
        )
        
        for check_name, _, detail in passed:
            print(f"O {check_name}: {detail}")
        
        for check_name, _, detail in failed:
            print(f"X {check_name}: {detail}")
            
            if check_name == "Elements in order":
                self._show_mismatches()
        
        print("\n" + "=" * 60)
        if success:
            print("!!! Data Transfer Complete !!!")
        else:
            print("!!! Data Transfer Failed !!!")
        print("=" * 60)
        
        return success
    
    def _format_list_preview(self, data, limit=10):
        preview = data[:limit]
        suffix = '...' if len(data) > limit else ''
        return f"{preview}{suffix}"
    
    def _show_mismatches(self, max_show=5):
        count = 0
        for i, (src, dst) in enumerate(zip(self.source_container, self.destination_container)):
            if src != dst:
                print(f"    Index {i}: expected {src}, got {dst}")
                count += 1
                if count >= max_show:
                    print(f"    (showing first {max_show} mismatches)")
                    break
    
    def display_summary(self):
        print(f"\nSource Container ({len(self.source_container)} items):")
        print(f"  {self._format_list_preview(self.source_container)}")
        
        print(f"\nDestination Container ({len(self.destination_container)} items):")
        print(f"  {self._format_list_preview(self.destination_container)}")


def main():
    source_data = [
        1, 2.5, 3, 4.7, 5, 6.3, 7, 8.9, 9, 10.1,
        11, 12.4, 13, 14.8, 15, 16.2, 17, 18.6, 19, 20.3,
        21, 22.9, 23, 24.5, 25, 26.7, 27, 28.1, 29, 30.4,
        31, 32.8, 33, 34.2, 35, 36.6, 37, 38.9, 39, 40.0,
        41, 42.3, 43, 44.7, 45, 46.5, 47, 48.8, 49, 50.2
    ]
    
    print_section_header("Producer-Consumer Problem")
    
    pc = ProducerConsumer(source_data)
    pc.run()    
    pc.verify()   
    pc.display_summary()


if __name__ == "__main__":
    main()