import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ProfileRoutingModule } from '@/profile/profile.routing.module'
import { ProfileViewComponent } from '@/profile/containers/profile-view/profile-view.component'
import { ProfileEditDocumentComponent } from '@/profile/components/profile-edit-document/profile-edit-document.component'
import { ProfileEditLimitationsComponent } from '@/profile/components/profile-edit-limitations/profile-edit-limitations.component'
import { ProfileEditDwellingComponent } from '@/profile/components/profile-edit-dwelling/profile-edit-dwelling.component'
import { ProfileEditSchoolComponent } from '@/profile/components/profile-edit-school/profile-edit-school.component'
import { ProfileEditDocumentRfinternationalpassportComponent } from '@/profile/components/profile-edit-document-rfinternationalpassport/profile-edit-document-rfinternationalpassport.component'
import { ProfileEditDocumentBirthcertificateComponent } from '@/profile/components/profile-edit-document-birthcertificate/profile-edit-document-birthcertificate.component'
import { ProfileEditDocumentForeignpassportComponent } from '@/profile/components/profile-edit-document-foreignpassport/profile-edit-document-foreignpassport.component'
import { ProfileEditDocumentOtherdocumentComponent } from '@/profile/components/profile-edit-document-otherdocument/profile-edit-document-otherdocument.component'
import { ProfileEditDocumentRfpassportComponent } from '@/profile/components/profile-edit-document-rfpassport/profile-edit-document-rfpassport.component'
import { ReactiveFormsModule } from '@angular/forms'
import { PhoneValidatorDirective } from '@/shared/phone.validator.directive'
import {
    ProfileEditDwellingRussiaComponent
} from '@/profile/components/profile-edit-dwelling-russia/profile-edit-dwelling-russia.component'
import {
    ProfileEditDwellingOtherComponent
} from '@/profile/components/profile-edit-dwelling-other/profile-edit-dwelling-other.component'


const COMPONENTS = [
    ProfileViewComponent,
    ProfileEditDocumentComponent,
    ProfileEditDwellingComponent,
    ProfileEditDwellingRussiaComponent,
    ProfileEditDwellingOtherComponent,
    ProfileEditLimitationsComponent,
    ProfileEditSchoolComponent,
    ProfileEditDocumentRfpassportComponent,
    ProfileEditDocumentRfinternationalpassportComponent,
    ProfileEditDocumentBirthcertificateComponent,
    ProfileEditDocumentForeignpassportComponent,
    ProfileEditDocumentOtherdocumentComponent
]


@NgModule( {
    declarations: [
        COMPONENTS,
        PhoneValidatorDirective
    ],
    imports: [
        SharedModule,
        ReactiveFormsModule,
        ProfileRoutingModule
    ]
} )
export class ProfileModule {}
