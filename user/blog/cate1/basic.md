---
title: basic test
date: 2024-4-5
category: cate1 multi_cate
description:
ps:
language: english
type: html
redirect:
---


# Image

![50](./pic/end.png)
![40,40](./pic/end.png,./pic/end.png)
![30,30,30](./pic/end.png,./pic/end.png,./pic/end.png)(description)

# Formula

## Inline Formula
The sum of two numbers: $a + b = b + a$

## Block Formula
### Single Line
$$ s = a $$

### Multi Line
$$
x + y = y + x
x^2 + y^2 = z^2
$$

# Code

Inline `code snippet` example.

# List

- First item
  - Nested item
    - Deeper item
      - Deepest item
    - Another nested item
      $$ E = mc^2 $$
      This is an inline formula $f(x) = x^2$.
      > Blockquote reference inside list.
      [Link to GitHub](https://github.com)

# Blockquote

> This is a single line blockquote.

> This is another blockquote.

> Multiple lines blockquote:
> 
> Line 1
> 
> Line 2

# code block

```cpp
int main(){
    int x = 0; // z
    string s = "sd";
}
```
```python
def fn():
    return 1
```
```txt
overflow overflow overflow overflow overflow overflow overflow overflow overflow overflow overflow overflow overflow 
```
- list
  ```txt
  margin left, but no left margin in this inlist block
  ```

- list
  .....
  ```txt
  .....
  ```
  .....

# complex

> [link-in-reference](https://github.com)
> 
> `code in reference`
> 
> formula in reference $ a + b = c$