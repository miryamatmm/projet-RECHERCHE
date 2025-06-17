// This component renders a customizable single-line text input field.
function TextInput({ value, onChange, placeholder = "Enter text", className = ""}) {
        return (
                <input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={`border-2 border-golden rounded px-3 py-2 mx-auto sm:w-[15%] focus:outline-none ${className}`}
                placeholder={placeholder}
                />
        );
}
      
export default TextInput;
