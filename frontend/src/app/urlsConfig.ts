class URLS {
    private root: string = '/me';

    public PROFILE: string = `${this.root}/profile`;
    public PROJECTS: string = `${this.root}/projects`;

    public PROJECT(projectId: string): string {
        return `${this.root}/projects/${projectId}`;
    }

    public PROJECT_SETTINGS(projectId: string): string {
        return `${this.root}/projects/${projectId}/settings`;
    }

    public BOARD(projectId: string): string {
        return `${this.root}/projects/${projectId}/board`;
    }

    public TASK(projectId: string, taskId: string): string {
        return `${this.root}/projects/${projectId}/board/${taskId}`;
    }

    public MEMBERS(projectId: string): string {
        return `${this.root}/projects/${projectId}/members`;
    }

    public GROUPS(projectId: string): string {
        return `${this.root}/projects/${projectId}/groups`;
    }

    public GROUP(projectId: string, groupId: string): string {
        return `${this.root}/projects/${projectId}/groups/${groupId}`;
    }
}

export const PRIVATE_URLS = new URLS()