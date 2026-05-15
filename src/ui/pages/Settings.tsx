export async function fetchToken(signal?: AbortSignal): Promise<TokenResponse> {
    const response = await fetch(`/api/v1/tokens`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`,
        },
        signal,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new ApiError(error.message, response.status);
    }

    return response.json();
}


export async function fetchRegister(signal?: AbortSignal): Promise<RegisterResponse> {
    const response = await fetch(`/api/v1/registers`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`,
        },
        signal,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new ApiError(error.message, response.status);
    }

    return response.json();
}


export async function fetchLogin(signal?: AbortSignal): Promise<LoginResponse> {
    const response = await fetch(`/api/v1/logins`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`,
        },
        signal,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new ApiError(error.message, response.status);
    }

    return response.json();
}


export const useMigration = () => {
    const [data, setData] = useState<MigrationData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const controller = new AbortController();
        fetchMigration(controller.signal)
            .then(setData)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
        return () => controller.abort();
    }, []);

    return { data, loading, error, refetch: () => fetchMigration() };
};
