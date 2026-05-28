export async function fetchUtils(signal?: AbortSignal): Promise<UtilsResponse> {
    const response = await fetch(`/api/v1/utilses`, {
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
