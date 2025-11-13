import java.util.ArrayList;
import java.util.NoSuchElementException;

public class PowerOfTwoMaxHeap {
    private final int numChildren; // 2^branchingExponent
    private final ArrayList<Integer> heap;

    public PowerOfTwoMaxHeap(int branchingExponent) {
        if (branchingExponent < 0 || branchingExponent > 10) {
            throw new IllegalArgumentException("branchingExponent must be between 0 and 10");
        }
        this.numChildren = 1 << branchingExponent; // 2^branchingExponent
        this.heap = new ArrayList<>();
    }

    public void insert(int value) {
        heap.add(value);
        siftUp(heap.size() - 1);
    }

    public int popMax() {
        if (heap.isEmpty()) {
            throw new NoSuchElementException("Heap is empty");
        }

        int max = heap.get(0);
        int last = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, last);
            siftDown(0);
        }

        return max;
    }

    private void siftUp(int index) {
        int current = index;
        while (current > 0) {
            int parent = (current - 1) / numChildren;
            if (heap.get(current) > heap.get(parent)) {
                swap(current, parent);
                current = parent;
            } else {
                break;
            }
        }
    }

    private void siftDown(int index) {
        int current = index;

        while (true) {
            int maxIndex = current;
            for (int i = 1; i <= numChildren; i++) {
                int child = numChildren * current + i;
                if (child < heap.size() && heap.get(child) > heap.get(maxIndex)) {
                    maxIndex = child;
                }
            }

            if (maxIndex != current) {
                swap(current, maxIndex);
                current = maxIndex;
            } else {
                break;
            }
        }
    }

    private void swap(int i, int j) {
        int tmp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, tmp);
    }

    public boolean isEmpty() {
        return heap.isEmpty();
    }

    public int size() {
        return heap.size();
    }

    // For debugging or testing
    public ArrayList<Integer> getHeapData() {
        return new ArrayList<>(heap);
    }
}
