export interface Emotion {
    name: string;
    is_generated: boolean;
}

export interface Tag {
    name: string;
    is_generated: boolean;
}

export interface Thought {
    id: number;
    title: string;
    content: string;
    status: string;
    is_generated: boolean;
    created_at: string;
    updated_at: string;
    emotions: Emotion[];
    tags: Tag[];
    links: number[];
}

export interface PaginatedResponse {
    total: number;
    page: number;
    limit: number;
    items: Thought[];
}
