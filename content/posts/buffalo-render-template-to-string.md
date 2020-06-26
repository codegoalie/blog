+++
date = "2019-03-06T15:43:24-05:00"
title = "Buffalo: Render a Template to String"
categories = ['Buffalo', 'Golang']
+++

The Golang web app framework, [Buffalo](https://gobuffalo.io), has a very good
templating system called [Plush](https://github.com/gobuffalo/plush). It adds
some nice features to the standard library templating specific to web applications
such as partials and local context. It's pretty intuitive if you're coming from
[Rails](https://rubyonrails.org/).

While the default setup makes rendering a template as a response to a request super
easy, using rendered template content elsewhere isn't so obvious.

<!-- more -->

Once you see it though, it's pretty straightforward to render a template to a string
within your action handler functions. Typically, we'd render a template like this:

```go
func homeHandler(c buffalo.Context) error {
	return c.Render(200, r.HTML("index.html"))
}
```

Today I needed to return some HTML in a JSON resposne to a webhook to display some of
our content within [HelpScout](https://www.helpscout.com/) for their dynamic app
integration. Originally, I had a simple link to render which I did as:

```go
render(200, r.JSON(
	struct {
		HTML string `json:"html"`
	}{
		HTML: fmt.Sprintf(`<a href="%s/users/%s">%s's profile</a>`, HOST, user.ID, user.FullName()),
	}),
)
```

This _barely_ worked for this case, but it did work. Then we wanted to add more info and
I wasn't willing to write HTML within a `Sprintf` call. There are three steps to render
an arbitrary template to a string: 

- Allocate an `io.Writer` to hold the rendered template's contents
- Render the template with a `Renderer`.
- Read the string from the `Writer`.

Here's the code:

```go
// allocate a buffer to render the template into
respBuf := &bytes.Buffer{}

// set any required values in the context (could be any `render.Data`)
c.Set("user", user)

// create the Renderer with the HTML method and call Render with the buffer and the necessary data
err = r.HTML("helpscout/sidebar.html", "layouts/zero.html").Render(respBuf, c.Data())
if err != nil {
	err = errors.WithStack(err)
	return err
}

// read the string out of the buffer (and in this case render it into a JSON response)
return c.Render(200, r.JSON(helpscoutResponse{HTML: respBuf.String()}))
```

That's it. It's pretty straightforward once you see it laid out. Hope this helps you (as
I'm sure it will help me in 6 months).

-- Chris
