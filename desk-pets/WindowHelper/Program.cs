using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text.Json;

class Program
{
    delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll")]
    static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

    struct RECT
    {
        public int Left, Top, Right, Bottom;
    }

    static void Main()
    {
        var windows = new List<object>();

        EnumWindows((hWnd, _) =>
        {
            if (!IsWindowVisible(hWnd)) return true;
            if (!GetWindowRect(hWnd, out var r)) return true;

            int w = r.Right - r.Left;
            int h = r.Bottom - r.Top;
            if (w <= 0 || h <= 0) return true;

            windows.Add(new {
                x = r.Left,
                y = r.Top,
                width = w,
                height = h
            });

            return true;
        }, IntPtr.Zero);

        Console.WriteLine(JsonSerializer.Serialize(windows));
    }
}
