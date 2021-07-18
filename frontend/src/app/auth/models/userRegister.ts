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


// TODO enforce email regex check and password security policy
export function validateUser( user: UserRegister ): boolean
{
    return !!( user.birthDate && user.surname && user.lastName && user.name && user.email && user.password )
}