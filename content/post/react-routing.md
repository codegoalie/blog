+++
date = "2017-06-03T12:11:17-04:00"
title = "Poor Man's React Router"
categories = ["React", "Javascript"]
+++

Recently at [Videofruit](1), we had a fun internal exercise of building an app
in single workday. That app ended up being an [Email Service Provider picker](2)
where you answer a series of questions and we recommend an email service
provider to meet your needs. In this post, we'll breakdown a simplified version
of that app focusing in on how we built a routing mechanism that is simple but
effective and uses no external dependencies.

<!-- more -->

The ESP picker app essentially consists of 4 pages: the landing page, a question
page, an email collection page, and the recommendation page. We've implemented
each of these pages as their own component and will now demonstrate how we
built a sub-system to decide which component to render and then renders it.

Surprise, surprise. In typical React fasion, we've implemented this component
selection logic wthin yet another component. This `PagePicker` component exists
near the root of the component hierarchy and has its own state which holds the
current component to render. `PagePicker` also defines a set of callbacks to
pass into each page in order to update that state and then render new
components.

```
import React, { Component } from "react";
import LandingPage from "./LandingPage";
import QuestionPage from "./QuestionPage";
import RecommendationPage from "./RecommendationPage";

import questions from "./questions.js";

class PagePicker extends Component {
  constructor(props) {
    super(props);

    this.state - {
      currentPage: "LandingPage",
      currentQuestion: 0
    };

    thisstartQuestions = this.startQuestions.bind(this);
    this.goToRecommendationPage = this.goToRecommendationPage.bind(this);
  }

  startQuestions() {
    this.setState({ currentPage: "QuestionPage", currentQuestion: 0 });
  }

  nextQuestion() {
    this.setState(prevState => {
      let nextQuestion= prevState.currentQuestion + 1;
      if (nextQuestion >= questions.length) {
        return { currentPage: "RecommendationPage" };
      } else {
        return { currentQuestion: nextQuestion };
      }
    });
  }

  calculateRecommendation() {
    // Your logic here
    return "super-awesome-recommendation";
  }

  render() {
    switch (this.state.currentPage) {
      case "LandingPage":
        return (
          <LandingPage 
            startQuestions={this.startQuestions}
          />
        );
        break;
      case "QuestionPage":
        return (
          <QuestionPage
            question={questions[this.state.currentQuestion]}
            nextQuestion={this.nextQuestion}
          />
        );
        break;
      case "RecommendationPage":
        return (
          <RecommendationPage
            recommendation={this.calculateRecommendation()}
          />
        );
        break;
    }
  }
}
```

As you can see, this approach is pretty straight forward and, most importantly,
it requires no third-party dependencies. As with any implementation, there are
caveats and trade-offs. Firstly, this approach does not work with an app where
you expect the number of pages to grow large. The `switch` statement can easily
get unweildy and hard to maintain.

If your app has pages which need to communicate to eachother directly, this 
approach could cause problems. Our app is very linear and each page is very
separate in both state and function. We take advantage of that in this
technique.

Overall, we're pleased with the declarative layout of this approach and that
the current page being shown is clearly defined in the state. Any of the
transition callbacks can contain more complex logic which would be fuctionally
encapsulated and easily testable. We hope you find some value in this technique
too.

Happy routing!

-- Chris


[1]: http://videofruit.com
[2]: http://whatemailserviceprovidershouldiuse.com
