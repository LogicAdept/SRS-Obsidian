<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие типы существуют в XSD?**

__Простой тип__ - это определение типа для значения, которое может использоваться в качестве содержимого элемента или атрибута. Этот тип данных не может содержать элементы или иметь атрибуты.

```xsd
<xsd:element name='price' type='xsd:decimal'/>
...
<price>45.50</price>
```

__Сложный тип__ - это определение типа для элементов, которые могут содержать атрибуты и другие элементы.

```xsd
<xsd:element name='price'>
    <xsd:complexType base='xsd:decimal'>
        <xsd:attribute name='currency' type='xsd:string'/>
    </xsd:complexType>
</xsd:element>
...
<price currency='US'>45.50</price>
```
