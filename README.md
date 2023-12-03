Simple queueing project

Get the repository and cd into the folder

```
git clone https://github.com/marco-create/queueing.git
cd queueing
```

Install requirements from the root directory

```
pip install -r requirements.txt
```
Now you can run it

```
mdone_one_node.py
```

or

```
mdone_two_node.py
```

<hr>

```mermaid
---
title: One-node M/D/1 system
---
  graph LR;
  A("Entry point")
  B("Leaving point")

      λ0 --> A
      λ1 --> node
      A --> node --> B
```


```mermaid
---
title: Two-node M/D/1 system
---
  graph LR;
    A("Entry point")
    B("Leaving point")

      λ0 --> A
      λ1 --> node#1
      λ2 --> node#2
      A --> node#1 --> node#2 --> B
```
