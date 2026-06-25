export async function fetchMigration(signal?: AbortSignal): Promise<MigrationResponse> {
    const response = await fetch(`/api/v1/migrations`, {
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
