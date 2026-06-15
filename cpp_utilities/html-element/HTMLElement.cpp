#include "HTMLElement.h"

using namespace std;

HTMLElement::HTMLElement(string _tag) : tag{_tag}
{}

HTMLElement* HTMLElement::setAttribute(const char*  attr, const char* val)
{
    attributes.emplace_back(attr,val);
    return this;
}

HTMLElement* HTMLElement::setSingle(bool _single)
{
    single = _single;
    return this;
}

void HTMLElement::generateContents(ostream& stream) const
{
    for(const shared_ptr<Element> e : contents)
        e->generate(stream);
}

void HTMLElement::generateAttributes(ostream& stream) const
{
    if(!attributes.empty())
        stream << " ";

    for(const auto& [key,value] : attributes)
        stream << key  << "='" << value << "' ";
}


void HTMLElement::generate(ostream& stream) const
{
    stream << "<" << tag;
    generateAttributes(stream);
    stream << ">";

    if(!single)
    {
        generateContents(stream);
        stream << "</" << tag << ">";
    }
}

shared_ptr<HTMLElement> make_HTMLElement(const char* tag)
{
    return make_shared<HTMLElement>(tag);
}
shared_ptr<TextElement> make_TextElement(const char* text)
{
    return make_shared<TextElement>(text);
}

ostream& operator<<(ostream& stream, const Element& elem)
{
    elem.generate(stream);
    return stream;
}
