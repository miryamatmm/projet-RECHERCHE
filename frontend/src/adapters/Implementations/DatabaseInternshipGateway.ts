import { Supervisor, University, Internship, Discipline, SearchParams } from "../../types";
import { InternshipGateway } from "../index";

export const API_URL = "http://127.0.0.1:8000"

export const gateway: InternshipGateway = {
	universities: async () => {
		return (await (await fetch(API_URL + "/universities")).json());
	},

	supervisors: async () => {
		return  (await (await fetch(API_URL + "/supervisors")).json());
	},

	disciplines: async () => {
		return (await (await fetch(API_URL + "/disciplines")).json());
	},

	search: async (params: SearchParams) => {
		// Prepare URLSearchParams and handle array parameters
		const queryParams = new URLSearchParams();

		// Manually handle arrays by joining them into comma-separated strings
		if (params.keywords) {
		params.keywords.forEach((keyword) => queryParams.append("keywords", keyword));
		}
		if (params.discipline_ids) {
		params.discipline_ids.forEach((id) => queryParams.append("discipline_ids", id));
		}
	
		// Add other parameters as normal
		if (params.start_date) queryParams.append("start_date", params.start_date);
		if (params.end_date) queryParams.append("end_date", params.end_date);
		if (params.university_id) queryParams.append("university_id", params.university_id);
		if (params.page) queryParams.append("page", params.page.toString());
		if (params.page_size) queryParams.append("page_size", params.page_size.toString());
	
		const response = await fetch(`${API_URL}/search?${queryParams.toString()}`);
		
		if (!response.ok) {
		throw new Error("Failed to fetch search results");
		}
		
		const data = await response.json();
	
		// Map the results to include the PDF path
		data.data = data.data.map((internship: any) => {
		internship.pdf_path = `${API_URL}/download/${internship.pdf_path}`;
		return internship;
		});
	
		return data;
	},

	upload: async(formData) => {
		const response = await fetch(API_URL + "/upload", {
			method: "POST",
			body: formData,
		});
		
		if (!response.ok) {
			throw new Error("Erreur lors de l'envoi des données");
		}
	},

	extract: async(formData) => {
		return await (await fetch(API_URL + "/extract", {
			method: "POST",
			body: formData,
		})).json();
	},

	posted_by: async (id) => {
		return (await (await fetch(API_URL + "/posted_by?supervisor_id=" + id)).json()).map((e) => {
			e.pdf_path = `${API_URL}/download/${e.pdf_path}`
			return e;
		});
	},

	delete: async (id) => {
		await (await fetch(API_URL + "/delete?internship_id=" + id)).json();
	},
};