export interface Emotion {
    name: string;
    is_generated: boolean;
}

export interface Tag {
    name: string;
    is_generated: boolean;
}


export interface Persona {
    id: number;
    name: string;
    age: number;
    gender: string;
}

export interface Thought {
    id: number;
    content: string;
    status: string;
    is_generated: boolean;
    action_orientation?: string;
    thought_type?: string;
    created_at: string;
    updated_at: string;
    emotions: Emotion[];
    tags: Tag[];
    links: number[];
    persona?: Persona;
}

export interface PaginatedResponse {
    total: number;
    page: number;
    limit: number;
    items: Thought[];
}
