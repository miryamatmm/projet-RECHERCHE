// This component renders a customizable multi-line text input field.
function TextArea({ value, onChange, placeholder = "Enter text", className = "" }) {
        return (
                <textarea
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={`border-2 border-golden rounded px-3 py-2 sm:w-[15%] focus:outline-none ${className}`}
                placeholder={placeholder}
                rows={4}
                />
        );
}
      
export default TextArea;
