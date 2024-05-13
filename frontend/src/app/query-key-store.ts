import {createQueryKeyStore} from "@lukemorales/query-key-factory";

export const queryKeys = createQueryKeyStore({
    profile: {
        edit: null
    },

    // todos: {
    //     detail: (todoId: string) => [todoId],
    //     list: (filters: TodoFilters) => ({
    //         queryKey: [{ filters }],
    //         queryFn: (ctx) => api.getTodos({ filters, page: ctx.pageParam }),
    //     }),
    // },
})