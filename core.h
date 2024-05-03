#include <vector>

template <typename T> class ArrayList{
  private:

  std::vector<T> list;

  public:

    T get(int index);
    void add(T item);
    T remove(int index);
    T set(int index, T item);
    int size();
    bool isEmpty();
    bool contains(T item);
    int indexOf(T item);
    void clear();

};