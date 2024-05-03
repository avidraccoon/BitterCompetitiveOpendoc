#include <iostream> 
#include <algorithm>
#include "core.h"
using namespace std; 


template <typename T> T ArrayList<T>::get(int index){
  return list[index];
}

template <typename T> void ArrayList<T>::add(T item){
  list.push_back(item);
}

template <typename T> T ArrayList<T>::remove(int index){
  T item = list[index];
  list.erase(list.begin() + index);
  return item;
}

template <typename T> T ArrayList<T>::set(int index, T item){
  T olditem = list[index];
  list[index] = item;
  return olditem;
}

template <typename T> int ArrayList<T>::size(){
  return list.size();
}

template <typename T> bool ArrayList<T>::isEmpty(){
  return list.empty();
}

template <typename T> bool ArrayList<T>::contains(T item){
  return count(list.begin(), list.end(), item) > 0;
}

template <typename T> int ArrayList<T>::indexOf(T item){
  auto it = find(list.begin(), list.end(), item); 
  if (it != list.end())  
  { 
    return it - list.begin(); 
  } 
  else { 
    return -1;
  } 
}

template <typename T> void ArrayList<T>::clear(){
  list.clear();
}
