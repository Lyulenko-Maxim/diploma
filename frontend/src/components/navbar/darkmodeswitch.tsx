import React from "react";
import {useTheme as useNextTheme} from "next-themes";
import {Switch} from "@nextui-org/switch";
import {MoonIcon, SunIcon} from "@nextui-org/shared-icons";

export const DarkModeSwitch = () => {
    const {setTheme, resolvedTheme} = useNextTheme();
    return (
        <Switch
            isSelected={resolvedTheme === "light"}
            onValueChange={(e) => setTheme(e ? "light" : "dark")}
            startContent={<MoonIcon/>}
            endContent={<SunIcon/>}

        />
    );
};
