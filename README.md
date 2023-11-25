﻿Simple queueing project

Install requirements from the root directory

```
pip install -r requirements.txt
```
Now you can run it

```
.\mdone_one_node.py
```

<hr>

```mermaid
---
title: One-node M/D/1 system
---
  graph LR;
  A("Entry point")
  B("Leaving point")
      A --> node --> B
```


```mermaid
---
title: Two-node M/D/1 system
---
  graph LR;
    A("Entry point")

    B("Leaving point")
      A --> node#1 --> node#2 --> B
```
