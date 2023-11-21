Simple queueing project

```mermaid
---
title: One-node M/D/1 system
---
  graph LR;
  A("Entry point")
  B(("UPF network"))
  C("Leaving point")
      A-->B --> C;
```


```mermaid
---
title: Two-node M/D/1 system
---
  graph LR;
    A("Entry point")
    subgraph Network
        direction LR
        UPF 
        MEC
    end
    C("Leaving point")
      A --> Network --> C
```