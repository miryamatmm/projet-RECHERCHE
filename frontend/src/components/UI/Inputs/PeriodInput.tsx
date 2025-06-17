import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

// This component allows the user to select a date range (start and end dates) using a month and year picker.
function PeriodInput ({range, setRange}) {
  return (
      <DatePicker className="border-2 border-golden w-full px-3 py-2 rounded outline-none focus:outline-none" selected={range[0]} 
        onChange={(dates) => { setRange(dates as [Date | null, Date | null])}}
        startDate={range[0]} endDate={range[1]} selectsRange dateFormat="MM/yyyy"
        placeholderText="Select a period"
        showMonthYearPicker
        popperPlacement="bottom-start"
        portalId="root"
      />
  );
};

export default PeriodInput;
