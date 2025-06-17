import { useState, useEffect } from "react";
import Select from 'react-select';
import clsx from "clsx";


const getThemeStyles = (isDarkMode) => ({
  control: (base, state) => ({
    ...base,
    backgroundColor: isDarkMode ? "#242424" : "#ffffff",
    color: isDarkMode ? "white" : "#333",
    border: "none",
    boxShadow: state.isFocused ? "0 0 4px rgba(178, 143, 79, 0.5)" : "none",
  }),
  menu: (base) => ({
    ...base,
    backgroundColor: isDarkMode ? "#242424" : "#ffffff",
    color: isDarkMode ? "white" : "#333",
  }),
  menuList: (base) => ({
    ...base,
    backgroundColor: isDarkMode ? "#242424" : "#ffffff",
    color: isDarkMode ? "white" : "#333",
  }),
  option: (base, state) => ({
    ...base,
    backgroundColor: state.isSelected
      ? isDarkMode
        ? "#373737"
        : "#e6e6e6"
      : state.isFocused
      ? isDarkMode
        ? "#2e2e2e"
        : "#f0f0f0"
      : isDarkMode
      ? "#242424"
      : "#ffffff",
    color: isDarkMode ? "white" : "#333",
    cursor: "pointer",
    "&:hover": {
      backgroundColor: isDarkMode ? "#373737" : "#e6e6e6",
      color: "white",
    },
  }),
  singleValue: (base) => ({
    ...base,
    color: isDarkMode ? "white" : "#333",
  }),
  placeholder: (base) => ({
    ...base,
    color: isDarkMode ? "#bbb" : "#777",
  }),
  multiValue: (base) => ({
    ...base,
    backgroundColor: isDarkMode ? "#373737" : "#ddd",
    color: "white",
  }),
  multiValueLabel: (base) => ({
    ...base,
    color: isDarkMode ? "white" : "#373236",
  }),
  multiValueRemove: (base) => ({
    ...base,
    color: isDarkMode ? "white" : "#373737", 
    "&:hover": {
      backgroundColor: "transparent", 
      color: isDarkMode ? "white" : "#373737", 
    },
  }),
  dropdownIndicator: (base, state) => ({
    ...base,
    color: state.isFocused ? (isDarkMode ? "#ffffff" : "#333") : (isDarkMode ? "#bbbbbb" : "#666"),
    "&:hover": {
      color: isDarkMode ? "#ffffff" : "#222",
    },
  }),
  indicatorsContainer: (base) => ({
    ...base,
    color: isDarkMode ? "#bbbbbb" : "#666",
  }),
});


// This component allows the user to select multiple options from a dropdown list.
const MultiSelect = ({options, setOptions, setSelectedOptions, selectedOptions = []}) => {
  
  const [isDarkMode, setIsDarkMode] = useState(
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleThemeChange = (e) => setIsDarkMode(e.matches);
    mediaQuery.addEventListener("change", handleThemeChange);
    return () => mediaQuery.removeEventListener("change", handleThemeChange);
  }, []);

  return (
  
      <Select
        onChange={(e) => {setSelectedOptions(e)}}
        value={selectedOptions}
        options={options}
        isMulti
        placeholder="Select subfields..."
        styles={getThemeStyles(isDarkMode)}
        className={clsx("border-2 rounded ", {
          "border-[#b28f4f] min-w-[60%] sm:min-w-[15%]": true,
        })}
      />

  );
};

export default MultiSelect;
