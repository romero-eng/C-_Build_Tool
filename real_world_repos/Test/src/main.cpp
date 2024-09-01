#include <fmt/core.h>
#include <fmt/color.h>
#include <fmt/chrono.h>


int main()
{
    auto now = std::chrono::system_clock::now();

    fmt::print("The answer is {}.\n", 42);
    fmt::print("I'd rather be {1} than {0}.\n", "right", "happy");
    fmt::print("Date and time: {}\n", now);
    fmt::print("Time: {:%H:%M}\n", now);
    fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "Hello, {}!\n", "world");
    fmt::print(fg(fmt::color::floral_white) | bg(fmt::color::slate_gray) | fmt::emphasis::underline, "Olá, {}!\n", "Mundo");
    fmt::print(fg(fmt::color::steel_blue) | fmt::emphasis::italic, "你好{}！\n", "世界");
}