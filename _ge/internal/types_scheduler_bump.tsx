export async function fetchExceptions(signal?: AbortSignal): Promise<ExceptionsResponse> {
    const response = await fetch(`/api/v1/exceptionses`, {
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
