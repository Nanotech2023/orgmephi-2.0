export type DocumentTypeEnum =  'RFPassport' | 'RFInternationalPassport' | 'ForeignPassport' | 'OtherDocument' | 'BirthCertificate';
export const DocumentTypeEnum = {
    RfPassport: 'RFPassport' as DocumentTypeEnum,
    RfInternationalPassport: 'RFInternationalPassport' as DocumentTypeEnum,
    BirthCertificate: 'BirthCertificate' as DocumentTypeEnum,
    ForeignPassport: 'ForeignPassport' as DocumentTypeEnum,
    OtherDocument: 'OtherDocument' as DocumentTypeEnum
}