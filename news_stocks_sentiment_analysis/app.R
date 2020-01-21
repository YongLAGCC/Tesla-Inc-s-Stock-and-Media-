Sys.setenv("LANGUAGE"="EN")
library(tidyverse)
library(shiny)

daily_price_with_scores <- read.csv(file = 'data/daily_price_with_scores.csv')
tweets_with_scores <- read.csv(file = 'data/Twitter_Data/unwashed_CNBC_TSLA_News_with_scores.csv') 

daily_price_with_scores <- daily_price_with_scores %>% 
  mutate(Date = as.Date(Date, origin = "1970-01-01"))

tweets_with_scores <- tweets_with_scores %>% 
  mutate(Date = as.Date(Date, origin = "1970-01-01"))

ui <- fluidPage(
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "style.css")
  ),
  # tags$script(src = "script.js"),
  htmlOutput(class="text-center", "title"),
  # column(id = "title", 8, offset = 4, titlePanel("Tesla Stock Price V.S. CNBC Tweets on Tesla")), 
  htmlOutput(class="text-center", "explaination"),
  fluidRow(
    column(width = 6, plotOutput("plot1", brush = brushOpts(id = "brush", direction = "x"))),
    column(width = 6, plotOutput("zoom"))
  ),
  dataTableOutput("info"),
  htmlOutput(class="text-center", "author")
  #, verbatimTextOutput("dbg")
) 

server <- function (input, output) {
  output$title <- renderText("<h1>Tesla Stock Price V.S. CNBC Tweets on Tesla</h1>")
  output$explaination <- renderText("<h3>Hello! Please select an area in the left to get zoomed in graph and related news.</h3>")
  
  brushed <- reactiveVal()
  res <- tweets_with_scores %>% 
    filter(Date >= as.Date("2015-11-10", origin = "1970-01-01")) %>% 
    filter(Date <= as.Date("2020-11-10", origin = "1970-01-01")) 
  brushed(res)
  
  observeEvent(input$brush, {
      res <- tweets_with_scores %>% 
        filter(Date >= as.Date(input$brush$xmin, origin = "1970-01-01")) %>% 
        filter(Date <= as.Date(input$brush$xmax, origin = "1970-01-01")) 
      
      brushed(res)
  })
  output$plot1 <- renderPlot(ggplot(daily_price_with_scores, aes(Date, Close))+
                               geom_line(size=1.2) +
                               theme(text = element_text(size=20), axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0))))
  output$zoom <- renderPlot({
    zoomed <- ggplot(daily_price_with_scores, aes(Date, Close, color="red")) + 
      geom_line(size=2) +
      guides(fill=FALSE, color=FALSE) +
      theme(text = element_text(size=20), axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)))
    
    if (!is.null(brushed()) & !is.null(input$brush$xmin)) {
      price_range <- daily_price_with_scores %>% 
        filter(Date >= as.Date(input$brush$xmin, origin = "1970-01-01")) %>% 
        filter(Date <= as.Date(input$brush$xmax, origin = "1970-01-01")) %>% 
        select(Close)
      
      min_price <- min(price_range$Close)
      max_price <- max(price_range$Close)
      
      left <- as.Date(input$brush$xmin, origin = "1970-01-01") %>% 
        format(., "%Y-%m-%d")
      right <- as.Date(input$brush$xmax, origin = "1970-01-01") %>% 
        format(., "%Y-%m-%d")
      
        zoomed <- zoomed + 
          xlim(as.Date(input$brush$xmin, origin = "1970-01-01"), as.Date(input$brush$xmax, origin = "1970-01-01")) +
          scale_y_continuous(breaks = pretty(price_range$Close, n = 10), limits=c(min_price, max_price)) 
    }
    zoomed
  })
  output$info <- renderDataTable(brushed(),options = list(pageLength = 10, autoWidth = TRUE))
  output$author <- renderText("Made by <a href='https://zackLight.com' target='_blank'>Zack Light</a>")
  # output$dbg <- renderText(res)
}

shinyApp(ui, server)