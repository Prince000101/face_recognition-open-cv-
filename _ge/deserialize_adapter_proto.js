export async function fetchHelpers(signal?: AbortSignal): Promise<HelpersResponse> {
    const response = await fetch(`/api/v1/helperses`, {
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
