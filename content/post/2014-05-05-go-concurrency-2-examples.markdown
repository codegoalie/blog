---
categories:
- golang
comments: true
date: 2014-06-14
layout: post
title: Go Concurrency by Example
---

Recently I've been dabling in Go. I was lured in by the lore of a purposefully
simple language with amazing concurrency features. While that is true, I have to
admit that I stayed around for the documentation. [Golang.org](http://golang.org)
has a this great [Tour](http://tour.golang.org) which walks you through the
basics of the language through interactive examples and exercises. Secondly, the
`godoc` command has a `--server` flag which spins up essentially a local copy of
golang.org but the docs pages also include any locale packages you have pulled
down, or that __you've developed__. Ok, enough gushing about Go documentation.

The end of the tour talks about concurrency and has some exercises to help you
learn by doing. I found this method very compelling and came up with two
different methods for handling concurrency in Go; each suited for slightly
different use cases.

<!-- more -->

## Primer

If you aren't familiar with concurrency in Go, this section is for you. I will
touch on some key points which are necessary to understand the examples below.
This is not an in-depth guide. I, myself, am still learning the ropes, but this
should cover us enough.

The idomatic way to handle concurrency in Go is through something called a
`goroutine`. A goroutine is something like a lightweight thread. They are cheap
to create and are ideal for small little jobs. Think of using goroutines as if
to say "Someone else go do this real quick." A thread will go do your bidding
and your program can continue to execute.

<pre>
<code class="Go">
func timer() {
  for i := 0; i < 10; i++ {
    time.Sleep(100 * time.Millisecond)
    fmt.Println(i)
  }
}

func main() {
  go timer()
  fmt.Println("Timer started")

  // wait for timer to complete
  time.Sleep(2000 * time.Millisecond)
}
</code>
</pre>


However, what about results from a goroutine? Many uses of concurrency involve a
collection phase where results from the concurrent tasks are reduced down to a
final result. This is where `channels` come in. Think of a channel like a typed
Unix pipe. Data written in at one end can be read from the other end.

Say we wanted to add all the digits from one to ten. We could let two goroutines
work on the first and half last each, then combine the individual results.

    func summer(start int, end int, c chan int) {
      sum := 0
      for i := start; i <= end; i++ {
        sum += i
      }
      c <- sum
    }

    func main() {
      c := make(chan int)

      go summer(1, 5, c)
      go summer(6, 10, c)

      // read the values from the channel
      first_half := <- c
      last_half :=  <- c

      fmt.Println(first_half, last_half, first_half + last_half)
    }


## Worker driven concurrency

Concurrency with a known amount of return values, like the above example, is
fairly straightforward, but also quite contrived. A (slightly) more realistic
example would include a case where the exact number of values to be sent through
a channel is unknown. Reads from channels will wait until a value is available
(similarly writes also wait for an empty space in a channel). The `range`
function will wait-read on a channel until the channel is closed. Closing a
channel should only be done on the writing end as trying to write to a closed
channel will `panic`. This wait-read cycle allows us to setup a loop waiting for
values on a channel and break out of the loop once the channel is closed.

In the example below we are calculating the decimal part of division in a
goroutine with the `decimal_divide` function. Since we won't know exactly how
many digits the decimal result will be we can wait on the digits and print them
as we get them. Once `decimal_divide` completes the division, it signals `main`
by closing the channel.

    func decimal_divide(numerator, denominator int, c chan int) {
      // do long division "by hand"
      for ; numerator != 0; numerator = numerator % denominator {
        numerator = numerator * 10
        // send the next calculated digit back to main
        c <- numerator / denominator
      }

      // all done; close the channel
      close(c)
    }


    func main() {
      numerator := 22
      denominator := 7

      // print the integer part of the result
      fmt.Print(numerator / denominator, ".")

      // calculate the decimal part digit by digit
      c := make(chan int)
      go decimal_divide(numerator, denominator, c)
      for digit := range c {
        fmt.Print(digit)
      }
      fmt.Print("\n")
    }


## Multi-worker concurrency

In the example above, is fairly "linear" since the input of the next step is the
output of the previous. It isn't straightforward to add additional working in
that case. However, let's look at a "fan out" style of problem where we won't
know the number of workers, nor the number of expected values. These kinds of
problems can be thought of as graph traversal problems.

Suppose we had a list of cities each with their own list of immediately
neighboring cities which were connected by roads.

    type cityList map[string][]string

    var list = cityList{
      "Cleveland":
        []string{"Columbus",
                 "Toledo",
                 "Pittsburg"},
      "Columbus":
        []string{"Cincinati",
                 "Cleveland",
                 "Pittsburg",
                 "Indinapolis"},
      "Toledo":
        []string{"Detroit",
                 "Columbus"},
      "London":
        []string{"Bristol",
                 "Sheffield"},
      "Sheffield":
          []string{"London",
                   "Bristol",
                   "Liverpool"}
    }


Using this information and a starting city, you could generate a list all the
cities which could be visited by car. Each time a city's neighbors are found,
a new goroutine can be used to fetch each neighbor's neighbors. Since, we won't
know, in advance, how many neighbors each city has or how many neighbors each
neighbor will have. We'll have to do some housekeeping of on our own to make
sure everyone is accounted. Further, after we see a city for the first time,
there's no reason to re-visit its neighbors again (and avoid graph loops).

    func main() {
        startingCity := "Cleveland";

        // keep track of cities we've visited to avoid infinite loops
        fetchedCities := map[string]bool{startingCity: true}

        // pass the neighbors after fetching
        c := make(chan []string)

        var fetchNeighbors = func(c chan []string, city string, list cityList) {
            if neighbors, ok := list[city]; ok {
              // if we've found the city on the map, send back the neighbors
              c <- neighbors;
            } else {
              // otherwise send no neighbors back
              // could be a good place for an error message, etc.
              c <- []string{};
            }
        }

        // track how many cities' neighbors are still to be fetched
        // start at one because of the starting city
        stillToFetch := 1;

        // go fetch the first set of neighbors
        go fetchNeighbors(c, startingCity, cityMap);

        // while we are still fetching neighbors
        for stillToFetch > 0 {

            // read the neighbors from the channel
            neighbors := <- c

            // track that we've fetched a set of neighbors
            stillToFetch--;

            for _, city := range neighbors {
                // if we haven't seen this city before
                if !fetchedCities[city] {
                    // mark it as seen
                    fetchedCities[city] = true

                    // now we have one more city to fetch
                    stillToFetch ++

                    // fetch
                    go fetchNeighbors(c, city, cityMap);

                    // print out the name of the neighbor as visitable
                    fmt.Println(city);
                }
            }
        }
    }

As you can see we've had to use the `stillToFetch` variable to keep track of
how many sets of neighbors to read from the channel. Each time we get a new set
of neighbors, we can subtract one to say that we've fetched neighbors. And on
the flip side, each new neighbor that we haven't seen yet, we add one to say
that we have another set of neighbors to fetch.

These examples show some basic techniques to work with concurrency in go and
many more techniques exist to create performant, robust applications. For full,
working examples please see [the
gist](https://gist.github.com/chrismar035/a59c50329ab7c87033c2)
to accompany this post. With the knowledge above, I hope you are inspired to
take advantage of the wonderful power amd simplicity of go concurrency. Please
link to any such work in the comments below.
