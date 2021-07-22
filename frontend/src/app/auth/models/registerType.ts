export interface RegisterType
{
    name: string,
    value: RegisterTypeEnum
}


export enum RegisterTypeEnum
{
    predUniver,
    enrollee,
    schoolOlymp,
    studentOlymp
}


export const RegisterTypes: RegisterType[] = [
    {
        name: 'Регистрация для поступления в Предуниверситарий НИЯУ МИФИ',
        value: RegisterTypeEnum.predUniver
    },
    {
        name: 'Регистрация абитуриентов для поступления в НИЯУ МИФИ (высшее и среднее профессиональное образование)',
        value: RegisterTypeEnum.enrollee
    },
    {
        name: 'Регистрация участников олимпиад школьников НИЯУ МИФИ',
        value: RegisterTypeEnum.schoolOlymp
    },
    {
        name: 'Регистрация участников студенческих олимпиад НИЯУ МИФИ',
        value: RegisterTypeEnum.studentOlymp
    }
]


