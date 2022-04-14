import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ProfileEditComponent } from '@/profile/containers/profile-edit/profile-edit.component'
import {
    ProfileEditUserinfoComponent
} from '@/profile/containers/profile-edit-userinfo/profile-edit-userinfo.component'
import { ProfileEditSchoolComponent } from '@/profile/containers/profile-edit-school/profile-edit-school.component'
import {
    ProfileEditPasswordComponent
} from '@/profile/containers/profile-edit-password/profile-edit-password.component'
import {
    ProfileEditDocumentComponent
} from '@/profile/components/profile-edit-document/profile-edit-document.component'
import {
    ProfileEditDwellingComponent
} from '@/profile/components/profile-edit-dwelling/profile-edit-dwelling.component'
import {
    ProfileEditDwellingRussiaComponent
} from '@/profile/components/profile-edit-dwelling-russia/profile-edit-dwelling-russia.component'
import {
    ProfileEditDwellingOtherComponent
} from '@/profile/components/profile-edit-dwelling-other/profile-edit-dwelling-other.component'
import {
    ProfileEditLimitationsComponent
} from '@/profile/components/profile-edit-limitations/profile-edit-limitations.component'
import {
    ProfileEditDocumentRfpassportComponent
} from '@/profile/components/profile-edit-document-rfpassport/profile-edit-document-rfpassport.component'
import {
    ProfileEditDocumentRfinternationalpassportComponent
} from '@/profile/components/profile-edit-document-rfinternationalpassport/profile-edit-document-rfinternationalpassport.component'
import {
    ProfileEditDocumentBirthcertificateComponent
} from '@/profile/components/profile-edit-document-birthcertificate/profile-edit-document-birthcertificate.component'
import {
    ProfileEditDocumentForeignpassportComponent
} from '@/profile/components/profile-edit-document-foreignpassport/profile-edit-document-foreignpassport.component'
import {
    ProfileEditDocumentOtherdocumentComponent
} from '@/profile/components/profile-edit-document-otherdocument/profile-edit-document-otherdocument.component'


export const PROFILE_COMPONENTS = [
    ProfileEditComponent,
    ProfileEditUserinfoComponent,
    ProfileEditSchoolComponent,
    ProfileEditPasswordComponent,
    ProfileEditDocumentComponent,
    ProfileEditDwellingComponent,
    ProfileEditDwellingRussiaComponent,
    ProfileEditDwellingOtherComponent,
    ProfileEditLimitationsComponent,
    ProfileEditDocumentRfpassportComponent,
    ProfileEditDocumentRfinternationalpassportComponent,
    ProfileEditDocumentBirthcertificateComponent,
    ProfileEditDocumentForeignpassportComponent,
    ProfileEditDocumentOtherdocumentComponent
]

export const PROFILE_ROUTES: Routes =
    [
        {
            path: 'profile', component: ProfileEditComponent, canActivate: [ AuthGuardService ],
            children: [
                {
                    path: '', pathMatch: 'full', redirectTo: 'userinfo'
                },
                {
                    path: 'userinfo',
                    component: ProfileEditUserinfoComponent
                },
                {
                    path: 'schoolinfo',
                    component: ProfileEditSchoolComponent
                },
                {
                    path: 'password',
                    component: ProfileEditPasswordComponent
                }
            ]
        }
    ]