import { Gender } from '@/users/models/participant/gender'
import { DocumentType, ForeignPassport, RussianPassport } from '@/users/models/participant/documents'
import { ForeignResidence, RussianResidence } from '@/users/models/participant/residence'
import { SpecialConditions } from '@/users/models/participant/specialConditions'


export interface ParticipantRegister
{
    email: string
    name: string
    surname: string
    lastName: string
    birthDate: Date | null
    gender: Gender
    birthPlace: string
    country: string
    phoneNumber: string
    documentType: DocumentType
    document: RussianPassport | ForeignPassport | null
    isRussianResident: boolean
    residence: ForeignResidence | RussianResidence | null
    specialConditions: SpecialConditions | null
}


export const emptyParticipant: ParticipantRegister = {
    email: '',
    name: '',
    surname: '',
    lastName: '',
    birthDate: null,
    gender: Gender.male,
    birthPlace: '',
    country: 'Россия',
    phoneNumber: '',
    documentType: DocumentType.russianPassport,
    document: null,
    isRussianResident: true,
    residence: null,
    specialConditions: null
}