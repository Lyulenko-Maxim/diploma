'use client'
import React, {FC} from 'react';
import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalFooter,
    Button
} from "@nextui-org/react";
import {useMutation} from "@tanstack/react-query";
import {authService} from "@/services/auth.service";
import {toast} from "sonner";
import {useRouter} from "next/navigation";

interface ILogoutModal {
    isOpen: boolean

    onOpenChange(): void,
}

const LogoutModal: FC<ILogoutModal> = ({onOpenChange, isOpen}) => {
        const {replace} = useRouter()

        const {mutate, isPending} = useMutation({
            mutationKey: ['logout'],
            mutationFn: () => authService.logout(),
            gcTime: 0,
            onSuccess() {
                replace('/auth/login')
                toast.success('Успешный выход')
            },
            onError(error) {
                toast.error('Произошла ошибка, попробуйте еще раз.')
            }
        })

        return (
            <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Вы уверены, что хотите выйти?</ModalHeader>
                            <ModalFooter>
                                <Button color="danger" onPress={() => {
                                    mutate();
                                    onClose();
                                }} isDisabled={isPending} isLoading={isPending}>Выйти
                                </Button>
                                <Button color="primary" onPress={onClose} isDisabled={isPending}>Отмена</Button>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>
        );
    }
;

export default LogoutModal;