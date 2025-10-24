library(readr)
Merged_Fares <- read_csv("/Users/brolinoconnell/Desktop/Johns Hopkins/Airlines_project/Fares_data/Merged_Fares .csv")
View(Merged_Fares)

str(Merged_Fares)

# This was a trash scatter to see intial data 
library(ggplot2)

ggplot(Merged_Fares, 
       aes(x = Year,
           y = as.numeric(gsub("[\\$,]", "", `Average Fare ($)`)),
           color = as.factor(Quarter))) +
  geom_point(alpha = 0.5, size = 1.5) +
  labs(
    title = "Average Fare by Quarter (1993–2025)",
    x = "Year",
    y = "Average Fare ($)",
    color = "Quarter"
  ) +
  theme_minimal(base_size = 14)



# Line Plot 
library(dplyr)
library(ggplot2)

Merged_Fares %>%
  mutate(
    Fare = as.numeric(gsub("[\\$,]", "", `Average Fare ($)`))
  ) %>%
  group_by(Year, Quarter) %>%
  summarise(Mean_Fare = mean(Fare, na.rm = TRUE), .groups = "drop") %>%
  mutate(Time = Year + (Quarter - 1) / 4) %>%   # create Time AFTER grouping
  ggplot(aes(x = Time, y = Mean_Fare, color = as.factor(Quarter))) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 1.5) +
  labs(
    title = "Average Fare by Quarter (1993–2025)",
    x = "Year",
    y = "Average Fare ($)",
    color = "Quarter"
  ) +
  theme_minimal(base_size = 14)


# Shocks Plot 
library(dplyr)
library(ggplot2)
library(scales)
library(zoo)

df <- Merged_Fares %>%
  mutate(
    Fare = as.numeric(gsub("[\\$,]", "", `Average Fare ($)`)),
    Passengers = as.numeric(gsub("[\\,]", "", `2024 Passengers (10% sample)`)),
    Time = Year + (Quarter - 1)/4
  ) %>%
  na.omit()

df_summary <- df %>%
  group_by(Year, Quarter) %>%
  summarise(
    Avg_Fare = mean(Fare, na.rm = TRUE),
    Avg_Passengers = mean(Passengers, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    Time = Year + (Quarter - 1)/4,
    Fare_Smoothed = rollmean(Avg_Fare, 4, fill = NA, align = "right"),
    Pax_Smoothed  = rollmean(Avg_Passengers, 4, fill = NA, align = "right")
  )

shocks <- data.frame(
  xmin = c(2008, 2020, 2022),
  xmax = c(2009, 2021, 2023),
  Shock = c("Financial Crisis (2008–09)", "COVID-19 (2020–21)", "Ukraine Invasion (2022–23)")
)

ggplot(df_summary, aes(x = Time)) +
  geom_rect(
    data = shocks,
    aes(xmin = xmin, xmax = xmax, ymin = -Inf, ymax = +Inf, fill = Shock),
    alpha = 0.2, inherit.aes = FALSE
  ) +
  geom_line(aes(y = Fare_Smoothed, color = "Average Fare ($)"), linewidth = 1.4) +
  geom_line(aes(y = Pax_Smoothed / 10000, color = "Passenger Volume (10% sample)"),
            linewidth = 1.2, linetype = "dashed") +
  geom_point(aes(y = Avg_Fare, shape = as.factor(Quarter)), color = "black", alpha = 0.5, size = 1.6) +
  scale_y_continuous(
    name = "Average Fare ($)",
    sec.axis = sec_axis(~.*10000, name = "Passenger Volume", labels = comma)
  ) +
  scale_x_continuous(breaks = seq(1993, 2025, 4)) +
  scale_color_manual(
    name = "Trend Line",
    values = c("Average Fare ($)" = "black", "Passenger Volume (10% sample)" = "steelblue4")
  ) +
  scale_fill_manual(
    name = "Shock Periods",
    values = c("Financial Crisis (2008–09)" = "#ffcc99",
               "COVID-19 (2020–21)" = "#99ccff",
               "Ukraine Invasion (2022–23)" = "#d9b3ff")
  ) +
  labs(
    title = "Airfare vs Passenger Volume (1993–2025)",
    x = "Year", shape = "Quarter"
  ) +
  theme_minimal(base_size = 15) +
  theme(
    panel.background = element_rect(fill = "gray97"),
    panel.grid.major = element_line(color = "gray85", size = 0.3),
    axis.title.y.left = element_text(color = "firebrick4", face = "bold"),
    axis.title.y.right = element_text(color = "steelblue4", face = "bold"),
    legend.position = "bottom",
    legend.key = element_blank(),
    legend.box = "vertical",
    plot.title = element_text(face = "bold", size = 17, hjust = 0.5),
    plot.subtitle = element_text(size = 13, hjust = 0.5)
  )


