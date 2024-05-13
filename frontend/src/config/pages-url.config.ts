class DASHBOARD {
    private root = '/me'

    HOME = this.root
    PROFILE = `${this.root}/profile`
}

export const DASHBOARD_PAGES = new DASHBOARD()


class AUTH {
    private root = '/auth'

    LOGIN = `${this.root}/login`
    REGISTER = `${this.root}/register`
    ACTIVATE = `${this.root}/activate`
}

export const AUTH_PAGES = new AUTH()