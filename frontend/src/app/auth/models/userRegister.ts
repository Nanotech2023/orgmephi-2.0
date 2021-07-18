export interface UserRegister
{
    registerNumber: string
    activationCode: string
    email: string
    password: string
    name: string
    surname: string
    lastName: string
    birthDate: Date | null
}


export function validateUser( user: UserRegister )
{
    return user.birthDate && user.surname && user.lastName && user.name && user.email && user.password
}