"use client";

import { useTheme } from "next-themes";
import { Toaster as Sonner, ToasterProps } from "sonner";

const Toaster = ({ ...props }: ToasterProps) => {
    const { theme = "system" } = useTheme();
    // Ensure theme is always a valid value
    const validTheme = (theme === "light" || theme === "dark" || theme === "system") ? theme : "light";
    return (
      <Sonner
        theme={validTheme}
        className="toaster group"
        style={
          {
            "--normal-bg": "var(--popover)",
            "--normal-text": "var(--popover-foreground)",
            "--normal-border": "var(--border)",
          } as React.CSSProperties
        }
        {...props}
      />
    );
  };

export { Toaster };
