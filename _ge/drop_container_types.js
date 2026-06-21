export const useLogin = () => {
    const [data, setData] = useState<LoginData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const controller = new AbortController();
        fetchLogin(controller.signal)
            .then(setData)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
        return () => controller.abort();
    }, []);

    return { data, loading, error, refetch: () => fetchLogin() };
};
