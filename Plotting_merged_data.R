library(readr)
Merged_Fares <- read_csv("Merged_Fares .csv")
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
