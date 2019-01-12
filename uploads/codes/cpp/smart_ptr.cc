// (C) Copyright 2018 by Liam Huang. All rights reserved.
// Author: Liam Huang <liamhuang0205@gmail.com>
// Date:   2018-01-13

#include <iostream>
#include <utility>

inline namespace liam {
class Point {
 private:
  int x_ = 0;
  int y_ = 0;

 public:
  Point() = default;
  Point(int x, int y) : x_{x}, y_{y} {}

 public:
  int x() const { return x_; }
  int y() const { return y_; }

  Point& x(int x) { x_ = x; return *this; }
  Point& y(int y) { y_ = y; return *this; }
};

class RefCount {
 private:
  size_t* count_ = nullptr;
  void try_decrease() {
    if (count_) {
      if (only()) {
        delete count_;
      } else {
        --(*count_);
      }
    } else {}
  }

 public:
  RefCount() : count_{new size_t(1)} {}
  RefCount(const RefCount& other) : count_{other.count_} { ++(*count_); }
  RefCount(RefCount&& other) : count_{other.count_} { other.count_ = nullptr; }
  RefCount& operator=(const RefCount& other) {
    try_decrease();
    count_ = other.count_;
    ++(*count_);
    return *this;
  }
  RefCount& operator=(RefCount&& other) {
    try_decrease();
    count_ = other.count_;
    other.count_ = nullptr;
    return *this;
  }
  ~RefCount() {
    try_decrease();
    count_ = nullptr;
  }

 public:
  bool only() const { return (1 == *count_); }
};

template<typename T>
class smart_ptr {
 public:
  using value_type = T;

 public:
  smart_ptr(value_type* pp) : value_{pp} {}
  smart_ptr(const value_type& p) : value_{new value_type(p)} {}
  smart_ptr(value_type&& p) : value_{new value_type{p}} {}

 public:
  smart_ptr() : value_{new value_type} {}
  smart_ptr(const smart_ptr& other) = default;
  smart_ptr(smart_ptr&& other) noexcept : value_{other.value_}, refc_{std::move(other.refc_)} {
    other.value_ = nullptr;
  }
  smart_ptr& operator=(const smart_ptr& other) {
    if (refc_.only()) {
      delete value_;
    }
    refc_  = other.refc_;
    value_ = other.value_;
    return *this;
  }
  smart_ptr& operator=(smart_ptr&& other) noexcept {
    if (refc_.only()) {
      delete value_;
    }
    refc_  = std::move(other.refc_);
    value_ = other.value_;
    other.value_ = nullptr;
    return *this;
  }
  ~smart_ptr() {
    if (value_ and refc_.only()) {
      delete value_;
      value_ = nullptr;
    }
  }

 public:
  value_type* operator->() const noexcept {
    return value_;
  }
  value_type& operator*() const noexcept {
    return *value_;
  }

 private:
  value_type* value_ = nullptr;
  RefCount refc_;
};

template<typename T, typename... Args>
smart_ptr<T> make_smart(Args&&... args) {
  return smart_ptr<T>(new T(std::forward<Args>(args)...));
}
}  // namespace liam

int main() {
  smart_ptr<Point> sp(make_smart<Point>(0, 1));
  std::cout << sp->x() << ' ' << (*sp).y() << '\n';
  return 0;
}

