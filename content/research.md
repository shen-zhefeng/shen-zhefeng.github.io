+++
title = "Research"
+++

# Some notes

## Include documents

1. document 1 [here](/papers/sample.pdf).
2. document 2 [here](/sample.pdf).


## Expandable block

### Native way: with `<details>` environment

<details>
<summary>Click this line to see more info</summary>

Here is the detailed information block.
You can even include **bold text** or [links][example_link].

</details>


### shortcode way: with `{% expand %}` shortcode

#### expandable.html

This is a normal paragraph, but {% expandable(trigger="if you click this line") %}
### Hidden Details
This block appears when the user clicks the text above. 
It supports **markdown** inside because we used `body | markdown`.
{% end %}
{% expandable(trigger="if you click this line") %}
### Hidden Details
This block appears when the user clicks the text above. 
It supports **markdown** inside because we used `body | markdown`.
{% end %}

line one

line two 

line three


1. What is this?
 
{% expandable(trigger="Abstract") %}
This block appears when the user clicks the text above. 
It supports **markdown** inside because we used `body | markdown`.
# 11
1
## 22
22
{% end %}
1. {% expandable(trigger="if you click this line") %}
This block appears when the user clicks the text above. 
It supports **markdown** inside because we used `body | markdown`.
{% end %}
1. {% expandable(trigger="if you click this line") %}
This block appears when the user clicks the text above. 
It supports **markdown** inside because we used `body | markdown`.
{% end %}


1. 1
2. 2
3. 3
4. 4
5. 5
6. 6
[example_link]:https://www.example.com
