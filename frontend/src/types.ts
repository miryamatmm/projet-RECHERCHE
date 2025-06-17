

export type Internship = {
    id: number;
    title: string;
	summary: string;
    pdf_path: string;
	start: string;
    end: string;
    disciplines: InternshipDiscipline[];
    keywords: InternshipKeyword[];
    supervisor_id?: number;
    supervisor: Supervisor;
}

export type InternshipKeyword = {
    id: number;
    name: string;
    internship_id: number;
}

export type InternshipDiscipline = {
    internship_id: number;
    discipline_id: number;
    discipline: Discipline;
}

export type SearchParams = {
    keywords: string[];
    discipline_ids: string[];
    start_date: string | undefined;
    end_date: string | undefined;
    university_id: string;
    page: number;
    page_size: number;
}

export const emptySearchPparams: SearchParams = {
    keywords: [],
    discipline_ids: [],
    start_date: null,
    end_date: null,
    university_id: "-1",
    page: 1,
    page_size: 10,
}

export type SearchResults = {
    data: Internship[],
    total: number,
    page: number,
    page_size: number,
    total_pages: number
}

export type InternshipAutoExtract = {
    title: string;
	summary: string;
	start: string;
    end: string;
    disciplines: Discipline[];
    keywords: string[];
}

export type Supervisor = {
    id: number;
    role: string;
    firstname: string;
    lastname: string;
    university_id: number;
    university: University;
    email: string;
}

export type University = {
    id: number;
    name: string;
    country: string;
    website: string;
}

export type Discipline = {
    id: number;
    name: string;
    parent_id: number | null;
}