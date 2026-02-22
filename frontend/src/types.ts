export interface Emotion {
    name: string;
    is_generated: boolean;
}

export interface Tag {
    name: string;
    is_generated: boolean;
}


export interface Topic {
    name: string;
    is_generated: boolean;
}


export interface Persona {
    id: number;
    name: string;
    age: number;
    gender: string;
    profile?: {
        topics: { name: string; emotions: string[] }[];
        thought_patterns: string;
        tags?: string[];
        thought_type?: string;
        action_orientation?: string;
    };
    additional_info?: Record<string, any>;
    source: 'manual' | 'derived' | 'movie_generated' | string;
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
    topics: Topic[];
    links: number[];
    persona?: Persona;
}

export interface PaginatedResponse {
    total: number;
    page: number;
    limit: number;
    items: Thought[];
}

export interface Message {
    id: number;
    content: string;
    is_generated: boolean;
    created_at: string;
    persona_id: number;
    conversation_id: number;
    persona?: Persona;
}

export interface Conversation {
    id: number;
    title: string;
    context: string;
    created_at: string;
    messages: Message[];
    personas: Persona[];
}

export interface MovieCharacter {
    movie_id: string;
    movie_title: string;
    movie_year: string;
    movie_imdb_rating: string;
    movie_genres: string[];
    character_id: string;
    character_name: string;
}

export interface MovieSearchResponse {
    results: MovieCharacter[];
}
